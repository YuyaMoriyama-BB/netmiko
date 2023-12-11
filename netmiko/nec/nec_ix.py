import re
from netmiko.base_connection import BaseConnection
from netmiko import log



class NecIXBase(BaseConnection):
    def check_config_mode(
        self, check_string: str = ")#", pattern: str = "", force_regex: bool = False
    ) -> bool:
        """Checks if the device is in configuration mode or not."""
        return super().check_config_mode(
            check_string=check_string, pattern=pattern, force_regex=force_regex
        )

    def config_mode(
        self,
        config_command: str = "svintr-config",
        pattern: str = "",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def exit_config_mode(self, exit_config: str = "exit", pattern: str = r"#") -> str:
        """Exit from configuration mode.

        :param exit_config: Command to exit configuration mode
        :type exit_config: str

        :param pattern: Pattern to terminate reading of channel
        :type pattern: str
        """
        output = ""
        if self.check_config_mode():
            self.write_channel(self.normalize_cmd(exit_config))
            # Make sure you read until you detect the command echo (avoid getting out of sync)
            if self.global_cmd_verify is not False:
                output += self.read_until_pattern(
                    pattern=re.escape(exit_config.strip())
                )
            if pattern:
                output += self.read_until_pattern(pattern=pattern)
            else:
                output += self.read_until_prompt(read_entire_line=True)
            if self.check_config_mode():
                #### In this series, if you are in Interface mode, cannot exit config mode unless you enter the "exit" command twice. ####
                self.write_channel(self.normalize_cmd(exit_config))
                if self.global_cmd_verify is not False:
                    output += self.read_until_pattern(
                        pattern=re.escape(exit_config.strip())
                    )
                if pattern:
                    output += self.read_until_pattern(pattern=pattern)
                else:
                    output += self.read_until_prompt(read_entire_line=True)
                #### 
                if self.check_config_mode():
                    raise ValueError("Failed to exit configuration mode")
                
        log.debug(f"exit_config_mode: {output}")
        return output

    def save_config(
        self,
        cmd: str = "copy running-config startup-config",
        confirm: bool = False,
        confirm_response: str = "",
    ) -> str:
        """Saves Config."""
        self.enable()
        if confirm:
            output = self._send_command_timing_str(
                command_string=cmd, strip_prompt=False, strip_command=False
            )
            if confirm_response:
                output += self._send_command_timing_str(
                    confirm_response, strip_prompt=False, strip_command=False
                )
            else:
                # Send enter by default
                output += self._send_command_timing_str(
                    self.RETURN, strip_prompt=False, strip_command=False
                )
        else:
            # Some devices are slow so match on trailing-prompt if you can
            output = self._send_command_str(
                command_string=cmd,
                strip_prompt=False,
                strip_command=False,
                read_timeout=100.0,
            )
        return output

    def send_command(self, *args, **kwargs):
        self.config_mode()
        return super().send_command(*args, **kwargs)

class NecIXSSH(NecIXBase):
    pass
