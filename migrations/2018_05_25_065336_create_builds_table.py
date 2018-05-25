from orator.migrations import Migration


class CreateBuildsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('builds') as table:
            table.increments('id')
            table.string('name').commit('项目名称')
            table.string('tag').commit('镜像tag')
            table.string('branch').nullable().commit('git分支')
            table.boolean('status').nullable().default(0)
            table.text('command').nullable().commit('运行容器的命令')
            table.string('host').nullable()
            table.string('port').nullable()
            table.string('notify').nullable()
            table.string('image_name').nullable()
            table.string('code_registry').nullable()
            table.boolean('send').nullable().default(0)
            table.text('dockerfile').nullable()
            table.index('name')
            table.index('tag')
            table.timestamps()


def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop('builds')
