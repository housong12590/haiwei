from orator.migrations import Migration


class CreateImagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('images') as table:
            table.increments('id')
            table.string('image_name')
            table.string('image_tag')
            table.string('git_branch').nullable()
            table.string('git_message').nullable()
            table.string('host').nullable()
            table.string('port').nullable()
            table.enum('dev', ['Y', 'N', 'F', 'D']).default('N')
            table.enum('pro', ['Y', 'N', 'F', 'D']).default('N')
            table.string('code_registry').nullable()
            table.string('pull_address')
            table.text('command').nullable()
            table.text('dockerfile').nullable()
            table.index('image_name')
            table.index('image_tag')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('images')
