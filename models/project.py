from orator import Model
from orator.orm import scope, accessor, mutator
from app.helper import get_environs
from . import Build, Environ
import json


class Project(Model):

    @scope
    def find_by_name(self, query, name):
        return query.where('name', name).get()

    @scope
    def find_by_image_name(self, query, name):
        return query.where('image_name', name)

    @accessor
    def environs(self) -> dict:
        base_dict, def_dict = self.__get_env()
        for key in def_dict.keys():
            if base_dict.get(key):
                def_dict[key] = base_dict[key]
        environs = self.get_raw_attribute('environs')
        if environs is None:
            pro_env_dict = {}
        else:
            pro_env_dict = json.loads(self.get_raw_attribute('environs'))
        def_dict.update(pro_env_dict)
        return def_dict

    @environs.mutator
    def set_environs(self, value):
        env_dict = value.copy()
        if not isinstance(env_dict, dict):
            raise TypeError('environ variables should be dict')
        base_dict, def_dict = self.__get_env()
        for key in list(env_dict.keys()):
            if env_dict[key] == base_dict.get(key) or env_dict[key] == def_dict.get(
                    key) or key is None:
                del env_dict[key]
        value = json.dumps(env_dict, sort_keys=False)
        self.set_raw_attribute('environs', value)

    @accessor
    def curr_tag(self):
        try:
            return self.get_raw_attribute('curr_tag')
        except KeyError:
            return None

    @curr_tag.mutator
    def set_curr_tag(self, value):
        try:
            last_tag = self.get_raw_attribute('curr_tag')
        except KeyError:
            last_tag = None
        self.set_raw_attribute('last_tag', last_tag)
        self.set_raw_attribute('curr_tag', value)

    # @accessor
    # def change(self):
    #     change_env = self.get_raw_attribute('change')
    #     return json.loads(change_env)
    #
    # @change.mutator
    # def set_change(self, value: dict):
    #     build = Build.find_by_tag(self.last_tag).first() if hasattr(self, 'last_tag') else None
    #     if build is None:
    #         self.set_raw_attribute('change', json.dumps(list([])))
    #     else:
    #         last_cmd = get_environs(build.command)
    #         diff_set = set(last_cmd.items()) ^ set(value.items())
    #         diff_set = set(item[0] for item in diff_set)
    #         value = json.dumps(list(diff_set))
    #         self.set_raw_attribute('change', value)

    def __get_env(self):
        build_obj = Build.find_by_tag(self.curr_tag).first()
        base_env_obj = Environ.find_default().first()
        base_env_dict = json.loads(base_env_obj.value) if base_env_obj else {}
        default_env_dict = get_environs(build_obj.command)
        return base_env_dict, default_env_dict

    def __repr__(self):
        return self.to_json()
