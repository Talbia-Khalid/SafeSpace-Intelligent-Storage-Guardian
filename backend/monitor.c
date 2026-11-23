#include "safespace.h"

#include <sys/inotify.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

volatile sig_atomic_t monitoring = 1;

void stop_monitoring(int signal_number)
{
    (void)signal_number;
    monitoring = 0;
}

void monitor_directory(char path[])
{
    int fd;
    int watch;

    char buffer[4096];

    monitoring = 1;

    // Create inotify instance
    fd = inotify_init();

    if (fd < 0)
    {
        perror("Error initializing inotify");
        return;
    }

    // Add directory watch
    watch = inotify_add_watch(
        fd,
        path,
        IN_CREATE | IN_MODIFY | IN_DELETE |
        IN_MOVED_FROM | IN_MOVED_TO
    );

    if (watch < 0)
    {
        perror("Error monitoring directory");
        close(fd);
        return;
    }

    struct sigaction action;
    memset(&action, 0, sizeof(action));
    action.sa_handler = stop_monitoring;
    sigemptyset(&action.sa_mask);
    action.sa_flags = 0;
    sigaction(SIGINT, &action, NULL);

    printf("\n===== FILE ACTIVITY MONITOR =====\n");
    printf("Monitoring folder: %s\n", path);
    printf("Press CTRL+C to stop monitoring.\n");
    printf("=================================\n");

    while (monitoring)
    {
        int length = read(fd, buffer, sizeof(buffer));

        if (length < 0)
        {
            if (errno == EINTR)
                continue;

            perror("Error reading events");
            break;
        }

        int i = 0;

        while (i < length)
        {
            struct inotify_event *event =
                (struct inotify_event *)&buffer[i];

            if (event->mask & IN_CREATE)
            {
                printf("[FILE CREATED] %s\n", event->name);
            }

            if (event->mask & IN_MODIFY)
            {
                printf("[FILE MODIFIED] %s\n", event->name);
            }

            if (event->mask & IN_DELETE)
            {
                printf("[FILE DELETED] %s\n", event->name);
            }

            if (event->mask & IN_MOVED_FROM)
            {
                printf("[FILE MOVED OUT] %s\n", event->name);
            }

            if (event->mask & IN_MOVED_TO)
            {
                printf("[FILE MOVED IN] %s\n", event->name);
            }

            i += sizeof(struct inotify_event) + event->len;
        }

        fflush(stdout);
    }

    inotify_rm_watch(fd, watch);

    close(fd);

    printf("\nFile monitoring stopped.\n");
}
