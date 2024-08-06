

class ProactiveScriptLanguage:
    """
    Represents the programming languages supported by Proactive
    
    supported_languages (dict)
    """

    supported_languages = {
        'Linux_Bash': 'bash', # keep for backward compatibility
        'Bash': 'bash',
        'Shell': 'shell',
        'Windows_Cmd': 'cmd',
        'DockerCompose': 'docker-compose',
        'DockerFile': 'dockerfile',
        'Kubernetes': 'kubernetes',
        'PHP': 'php',
        'VBScript': 'vbscript',
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
        return language in self.supported_languages.values()

    def __getattr__(self, name):
        normalized_name = name.lower()
        for key, value in self.supported_languages.items():
            if key.lower() == normalized_name or value.lower() == normalized_name:
                return value
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def linux_bash(self):
        return self.supported_languages["Linux_Bash"]

    def bash(self):
        return self.supported_languages["Bash"]

    def shell(self):
        return self.supported_languages["Shell"]

    def windows_cmd(self):
        return self.supported_languages["Windows_Cmd"]

    def docker_compose(self):
        return self.supported_languages["DockerCompose"]

    def dockerfile(self):
        return self.supported_languages["DockerFile"]

    def kubernetes(self):
        return self.supported_languages["Kubernetes"]

    def php(self):
        return self.supported_languages["PHP"]

    def vbscript(self):
        return self.supported_languages["VBScript"]

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

