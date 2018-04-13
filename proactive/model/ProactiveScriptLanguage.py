

class ProactiveScriptLanguage:
  language = {
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
    return self.language

  def linux_bash(self):
    return self.language["Linux_Bash"]

  def windows_cmd(self):
    return self.language["Windows_Cmd"]

  def docker_compose(self):
    return self.language["DockerCompose"]

  def scalaw(self):
    return self.language["Scalaw"]

  def groovy(self):
    return self.language["Groovy"]

  def javascript(self):
    return self.language["Javascript"]

  def jython(self):
    return self.language["Jython"]

  def python(self):
    return self.language["Python"]

  def ruby(self):
    return self.language["Ruby"]

  def perl(self):
    return self.language["Perl"]

  def powershell(self):
    return self.language["PowerShell"]

  def r(self):
    return self.language["R"]

