#include "safespace.h"

#include <sys/inotify.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>

#define ACTIVITY_WINDOW 10

#define CREATE_LIMIT 10
#define DELETE_LIMIT 5
#define MODIFY_LIMIT 20

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

    int created = 0;
    int deleted = 0;
    int modified = 0;

    int create_alert = 0;
    int delete_alert = 0;
    int modify_alert = 0;

    time_t window_start = 0;

    monitoring = 1;

    fd = inotify_init();

    if (fd < 0)
    {
        perror("Error initializing inotify");
        return;
    }

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

    printf("\n===== INTELLIGENT ACTIVITY GUARDIAN =====\n");
    printf("Monitoring folder: %s\n", path);
    printf("Activity detection window: %d seconds\n",
           ACTIVITY_WINDOW);
    printf("Press CTRL+C to stop monitoring.\n");
    printf("=========================================\n");

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

            if (!(event->mask & IN_ISDIR))
            {
                time_t current_time = time(NULL);

                if (window_start == 0 ||
                    difftime(current_time, window_start) >=
                    ACTIVITY_WINDOW)
                {
                    created = 0;
                    deleted = 0;
                    modified = 0;

                    create_alert = 0;
                    delete_alert = 0;
                    modify_alert = 0;

                    window_start = current_time;
                }

                if (event->mask & IN_CREATE)
                {
                    printf("[FILE CREATED] %s\n", event->name);
                    created++;
                }

                if (event->mask & IN_MODIFY)
                {
                    printf("[FILE MODIFIED] %s\n", event->name);
                    modified++;
                }

                if (event->mask & IN_DELETE)
                {
                    printf("[FILE DELETED] %s\n", event->name);
                    deleted++;
                }

                if (event->mask & IN_MOVED_FROM)
                {
                    printf("[FILE MOVED OUT] %s\n", event->name);
                }

                if (event->mask & IN_MOVED_TO)
                {
                    printf("[FILE MOVED IN] %s\n", event->name);
                }

                /* GUARDIAN ACTIVITY ANALYSIS */

                if (created >= CREATE_LIMIT && !create_alert)
                {
                    printf("\n[GUARDIAN NOTICE] Rapid file creation detected!\n");
                    printf("Files created in current window: %d\n\n",
                           created);

                    create_alert = 1;
                }

                if (deleted >= DELETE_LIMIT && !delete_alert)
                {
                    printf("\n[GUARDIAN HIGH RISK] Rapid file deletion detected!\n");
                    printf("Files deleted in current window: %d\n\n",
                           deleted);

                    delete_alert = 1;
                }

                if (modified >= MODIFY_LIMIT && !modify_alert)
                {
                    printf("\n[GUARDIAN NOTICE] Repeated file modifications detected!\n");
                    printf("Modification events in current window: %d\n\n",
                           modified);

                    modify_alert = 1;
                }
            }

            i += sizeof(struct inotify_event) + event->len;
        }

        fflush(stdout);
    }

    inotify_rm_watch(fd, watch);

    close(fd);

    printf("\nActivity monitoring stopped.\n");
}
