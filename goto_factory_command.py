import sublime, sublime_plugin, re, os

class GotoFactoryCommand(sublime_plugin.TextCommand):
  _RAILS_BASE_REGEXP = re.compile(r'^(\/.*)\/app\/*')
  _RAILS_MODEL_REGEXP = re.compile(r'\/app\/models\/(.*\.rb$)')
  _RAILS_MODEL_SPEC_REGEXP = re.compile(r'\/spec\/models\/(.*\.rb$)')

  def run(self, edit):
    file_name = self.view.file_name()
    rails_base_path = self._extract_rails_base_path(file_name)

    model = self._extract_model(file_name)
    model_test = self._extract_model_test(file_name)

    factory = ''

    if model:
      factory = self._generate_factory_file(rails_base_path, model)
    elif model_test:
      factory = self._generate_factory_file(rails_base_path, model_test)

    if factory:
      self.view.window().open_file(factory)


  def _extract_model_test(self, file_name):
    match_data = GotoFactoryCommand._RAILS_MODEL_SPEC_REGEXP.findall(file_name)
    if match_data:
      return match_data[0]
    else:
      return None


  def _extract_model(self, file_name):
    match_data = GotoFactoryCommand._RAILS_MODEL_REGEXP.findall(file_name)
    if match_data:
      return match_data[0]
    else:
      return None


  def _extract_rails_base_path(self, file_name):
    match_data = GotoFactoryCommand._RAILS_BASE_REGEXP.findall(file_name)
    if match_data:
      return match_data[0]
    else:
      return None


  def _generate_factory_file(self, rails_base, model_or_test):
    factory = model_or_test.replace('_test', '')
    factory = factory.replace('.rb', 's.rb')
    return os.path.join(rails_base, 'spec', 'factories', factory)
