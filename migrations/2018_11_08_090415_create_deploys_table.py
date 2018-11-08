from orator.migrations import Migration


class CreateDeploysTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('deploys') as table:
            table.increments('id')
            table.integer('project_id')
            table.string('image_tag')
            table.text('remark').nullable()
            table.enum('dev', ['Y', 'N', 'F', 'D']).default('N')
            table.enum('pro', ['Y', 'N', 'F', 'D']).default('N')
            table.index('project_id')
            table.index('image_tag')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('deploys')
