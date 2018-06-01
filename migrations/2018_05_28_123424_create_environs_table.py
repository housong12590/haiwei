from orator.migrations import Migration


class CreateEnvironsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('environs') as table:
            table.increments('id')
            table.string('name')
            table.string('key')
            table.string('value').default('')
            table.string('desc').nullable()
            table.integer('parent_id', unsigned=True).default(0)
            table.integer('project_id', unsigned=True).default(0)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('environs')
