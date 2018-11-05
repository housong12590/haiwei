from orator.migrations import Migration


class CreateOriginProjectsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('origin_projects') as table:
            table.integer('id')
            table.string('name')
            table.string('desc').nullable()
            table.primary('id')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('origin_projects')
