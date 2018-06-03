from orator.migrations import Migration


class CreateEnvironsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('environs') as table:
            table.increments('id')
            table.string('name').nullable()
            table.text('value').nullable()
            table.string('desc').nullable()
            table.boolean('default').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('environs')
