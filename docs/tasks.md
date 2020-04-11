# Configure tasks
> Setup tasks for Unicron to manage

Follow instructions below to add add executables (or symlinks to executables) in the _targets_ directory. You might want to actually the example script as below - you can use it to confirm Unicorn works as expected and see what output it gives.

1. Start from the repo root.
2. Create a script and make it executable. e.g.
    ```bash
    $ echo -e '#!/bin/bash\necho "Hello world!"\n' > unicron/var/targets/hello.sh
    $ chmod +x unicron/var/targets/hello.sh
    ```
3. Run the script directly to check that it works fine. e.g
    ```bash
    $ unicron/var/targets/hello.sh
    Hello world!
    ```

Repeat setup for all tasks that you want automated through _Unicron_. Once you have one executable script setup, you can easily copy the file for each new task.
