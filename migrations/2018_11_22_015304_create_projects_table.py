from orator.migrations import Migration


class CreateProjectsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('projects') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('desc').nullable()
            table.string('image_name').nullable()
            table.string('image_prefix').nullable()
            table.string('last_tag').nullable()
            table.string('new_tag').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('projects')
