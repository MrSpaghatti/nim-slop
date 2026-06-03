import unittest
import generate_dataset

class TestGenerateDataset(unittest.TestCase):
    def setUp(self):
        # Save the original state of TEMPLATES
        self.original_templates = list(generate_dataset.TEMPLATES)
        # Clear the global TEMPLATES list
        generate_dataset.TEMPLATES.clear()

    def tearDown(self):
        # Restore the original state of TEMPLATES
        generate_dataset.TEMPLATES.clear()
        generate_dataset.TEMPLATES.extend(self.original_templates)

    def test_register_template(self):
        # Dummy arguments
        dummy_name = "test_template"
        dummy_tags = ["tag1", "tag2"]
        dummy_prompts = ["prompt 1", "prompt 2"]
        dummy_thinking = "thinking process"
        dummy_code = "print('hello')"
        dummy_generator = lambda: [{"var": 1}]

        # Call the function
        generate_dataset.register_template(
            name=dummy_name,
            tags=dummy_tags,
            prompts=dummy_prompts,
            thinking=dummy_thinking,
            code=dummy_code,
            generator=dummy_generator
        )

        # Assert that the list has exactly one item
        self.assertEqual(len(generate_dataset.TEMPLATES), 1)

        # Assert that the attributes of the item match the dummy arguments
        registered_template = generate_dataset.TEMPLATES[0]
        self.assertEqual(registered_template.name, dummy_name)
        self.assertEqual(registered_template.tags, dummy_tags)
        self.assertEqual(registered_template.prompts, dummy_prompts)
        self.assertEqual(registered_template.thinking, dummy_thinking)
        self.assertEqual(registered_template.code, dummy_code)
        self.assertEqual(registered_template.generator, dummy_generator)

if __name__ == '__main__':
    unittest.main()
