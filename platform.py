from platformio.managers.platform import PlatformBase

class PropellerPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        return PlatformBase.configure_default_packages(self, variables,
                                                       targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        if "tools" not in debug:
            debug['tools'] = {}
        debug["tools"]["gdbstub"] = {
                "init_cmds": [
                    "define pio_reset_halt_target",
                    "end",
                    "define pio_reset_run_target",
                    "end",
                    "target remote |~/.platformio/packages/toolchain-propeller/bin/gdbstub",
                    "set remote hardware-breakpoint-limit 1",
                    "$INIT_BREAK"
                ],
                "load_cmd": "preload",
                "onboard": True
            }
        board.manifest['debug'] = debug
        return board