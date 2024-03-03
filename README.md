# mihomo-start

[原神](https://wiki.metacubex.one/)，启动

## File Structure

### stand-alone

```bash
├── mihomo                                                  [require download]
├── geo*.(dat|metadb)                                       [require download]
├── mihomo-start                    * MAIN *
│   ├── install
│   │   ├── *.install.py
│   │   ├── *.service
│   │   ├── *.timer
│   │   ├── *.subscribe.sh
│   │   ├── util.py
│   ├── scripts
│   │   ├── *.py
│   ├── templates
│   │   ├── config.template.yaml
├── metacubexdb                                             [require download]
│   ├── *.*
├── subscribe.json                                          [require prepare]
├── subscribe_cache                 * GENERATED LATER *
│   ├── 
├── cache.db                        * GENERATED LATER *
├── <*>.subscribe.sh                * GENERATED INSTALL *
├── <*>.service                     * GENERATED INSTALL *
├── <*>.timer                       * GENERATED INSTALL *
```

- core binary should be downloaded manually.
- geo*.(dat|metadb) should be downloaded manually.
- metacubexdb should be downloaded manually from gh-pages branch and rename to `metacubexdb`.
- subscribe.json should be prepared with your own subscription information.
- put `mihomo-start` to corresponding directory 
- run `mihomo-start/install/*.install.py` to install service and timer
  - follow the guide of `mihomo-start/install/*.install.py`. notice that value in `[ ]` means default and if you want to use default value, you can just press enter.
  - `<*>.subscribe.sh` ,  `<*>.service`, `<*>.timer` will be generated.
  - copy service and timer to corresponding directory as `mihomo-start/install/*.install.py` guide at the end.
- modify `mihomo-start/templates/config.template.yaml` if necessary. 
  - this modification can be done anytime before a service is started.
- try to run `<*>.subscribe.sh` to test if tools are working.
- enable and start sevice.

### docker

```bash
/
├── usr 
│   ├── local
│   │   ├── bin
│   │   │   ├── mihomo
├── var 
│   ├── lib
│   │   ├── <*>
│   │   │   ├── mihomo-start
│   │   │   │   ├── scripts
│   │   │   │   │   ├── *.py
│   │   │   │   ├── templates
│   │   │   │   │   ├── config.template.yaml
│   │   │   │   ├── docker_launch.sh
│   │   │   ├── geo*.(dat|metadb)
│   │   │   ├── metacubexdb
│   │   │   │   ├── *.*
│   │   │   ├── subscribe.json                                              [require prepare and bind from host] 
│   │   │   ├── subscribe_cache                     * GENERATED LATER *     [require bind to host]
│   │   │   │   ├──                                 * GENERATED LATER *     [require bind to host]
│   │   │   ├── cache.db                            * GENERATED LATER *     [require bind to host]
```