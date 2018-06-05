from orator.migrations import Migration


class CreateBuildsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('builds') as table:
            table.increments('id')
            table.string('name')
            table.string('tag')
            table.string('branch').nullable()
            table.integer('status').default(0)  # 0:不需要部署 1:等待部署 2:部署成功 3:部署失败
            table.text('command').nullable()
            table.string('host').nullable()
            table.string('port').nullable()
            table.string('notify').nullable()
            table.string('image_name').nullable()
            table.string('code_registry').nullable()
            table.boolean('send').nullable().default(0)
            table.text('dockerfile').nullable()
            table.string('message').nullable()
            table.index('name')
            table.index('tag')
            table.timestamps()


def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop('builds')
