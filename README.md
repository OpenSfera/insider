# insider

opensfera try to regulate itself, if something seem to fail for a long time `insider` is the one who
tell you about it.

### How works

listen on `local/manager` for sensors alert. if the alert fails to solve it in a while,
it publish on `local/alarm`. Publish on `local/alarm` is consider as **ask to human**

There are 2 different zones, WARNING and DANGER. On WARNING it wait about 5 minutes to ask human,
on DANGER it ask after an alert's confirmation.

If the alert do not turn off in `insider_time_interval` it will ask again.

| WARNING ZONE                 |
|------------------------------|
| t1 < t1_min  OR t1 > t1_max  |
| h1 < h1_min  OR h1 > h1_max  |
| ligths fails                 |
| service down                 |

| DANGER ZONE                  |
|------------------------------|
| t1 < 5°C OR t1 > 50°C        |
| h1 < 5%  OR h1 > 90%         |


### HEY, THATS NOT A BUG, IT'S A FEATURE

`insider` is listening on paramedic's alerts. If your sfera configurations are off the danger zones
`paramedic` do not send alerts and no one will notice.

The danger zone is intended to prevent fire or flood BUT if you want to go there... well, is up to you.

### TODO

- channel to ask handled by plugins
