from orator.migrations import Migration


class CreateDeploysTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('deploys') as table:
            table.increments('id')
            table.string('image_tag')
            table.string('image_name')
            table.text('remark').nullable()
            table.enum('dev', ['Y', 'N', 'F', 'D']).default('N')
            table.enum('pro', ['Y', 'N', 'F', 'D']).default('N')
            table.string('type')
            table.index('image_tag')
            table.integer('user_id')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('deploys')
