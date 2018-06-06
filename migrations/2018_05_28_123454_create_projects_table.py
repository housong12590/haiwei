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
            table.string('curr_tag').nullable()
            table.string('last_tag').nullable()
            table.text('environs').nullable()
            table.text('change').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('projects')
