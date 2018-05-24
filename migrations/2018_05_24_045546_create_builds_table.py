from orator.migrations import Migration


class CreateBuildsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('builds') as table:
            table.increments('id')
            table.string('name').commit('项目名称')
            table.string('tag').nullable().commit('镜像tag')
            table.string('branch').nullable().commit('git分支')
            table.string('status').nullable().commit('构建状态')
            table.text('command').nullable().commit('运行容器的命令')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('builds')
