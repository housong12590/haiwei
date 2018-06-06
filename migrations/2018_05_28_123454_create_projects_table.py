from orator.migrations import Migration


class CreateProjectsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('projects') as table:
            table.integer('id', unsigned=False)
            table.string('name')
            table.string('desc').nullable()
            table.string('image_name').nullable()
            table.string('last_tag').nullable()
            table.string('address').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('projects')
