

class ProactiveScriptLanguage:
    """
      Represents the programming languages supported by Proactive

      supported_languages (dict)
    """

    supported_languages = {
        'Linux_Bash': 'bash',
        'Windows_Cmd': 'cmd',
        'DockerCompose': 'docker-compose',
        'Scalaw': 'scalaw',
        'Groovy': 'groovy',
        'Javascript': 'javascript',
        'Jython': 'python',
        'Python': 'cpython',
        'Ruby': 'ruby',
        'Perl': 'perl',
        'PowerShell': 'powershell',
        'R': 'R'
    }

    def get_supported_languages(self):
        return self.supported_languages

    def is_language_supported(self, language):
        return True if language in self.supported_languages.values() else False

    def linux_bash(self):
        return self.supported_languages["Linux_Bash"]

    def windows_cmd(self):
        return self.supported_languages["Windows_Cmd"]

    def docker_compose(self):
        return self.supported_languages["DockerCompose"]

    def scalaw(self):
        return self.supported_languages["Scalaw"]

    def groovy(self):
        return self.supported_languages["Groovy"]

    def javascript(self):
        return self.supported_languages["Javascript"]

    def jython(self):
        return self.supported_languages["Jython"]

    def python(self):
        return self.supported_languages["Python"]

    def ruby(self):
        return self.supported_languages["Ruby"]

    def perl(self):
        return self.supported_languages["Perl"]

    def powershell(self):
        return self.supported_languages["PowerShell"]

    def r(self):
        return self.supported_languages["R"]

