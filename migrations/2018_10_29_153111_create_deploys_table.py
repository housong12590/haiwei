from orator.migrations import Migration


class CreateDeploysTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('deploys') as table:
            table.increments('id')
            table.string('image_tag')
            table.
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('deploys')
