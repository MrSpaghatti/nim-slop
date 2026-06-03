import pytest
from unittest.mock import patch
from generate_dataset import generate_examples, TemplateDef

@pytest.fixture
def empty_templates():
    with patch('generate_dataset.TEMPLATES', []):
        yield

def test_generate_examples_empty_templates(empty_templates):
    """Test that function returns empty list when TEMPLATES is empty."""
    examples = generate_examples(target_total=10)
    assert examples == []

def test_generate_examples_string_code():
    """Test template with string code."""
    t = TemplateDef(
        name="test_string",
        tags=["tag1"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code="Code: {var}",
        generator=lambda: [{"var": "A"}]
    )
    with patch('generate_dataset.TEMPLATES', [t]):
        examples = generate_examples(target_total=10)
        assert len(examples) == 1
        assert examples[0]["prompt"] == "Prompt: A"
        assert examples[0]["thinking"] == "Thinking: A"
        assert examples[0]["nim_code"] == "Code: A"
        assert examples[0]["tags"] == ["tag1"]

def test_generate_examples_callable_code():
    """Test template with callable code."""
    t = TemplateDef(
        name="test_callable",
        tags=["tag2"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code=lambda p: f"Callable code: {p['var']}",
        generator=lambda: [{"var": "B"}]
    )
    with patch('generate_dataset.TEMPLATES', [t]):
        examples = generate_examples(target_total=10)
        assert len(examples) == 1
        assert examples[0]["nim_code"] == "Callable code: B"

def test_generate_examples_deduplication():
    """Test that identical code outputs are deduplicated."""
    t = TemplateDef(
        name="test_dedup",
        tags=["tag3"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code="Same code", # Always produces same code
        generator=lambda: [{"var": "1"}, {"var": "2"}, {"var": "3"}]
    )
    with patch('generate_dataset.TEMPLATES', [t]):
        # Even though there are 3 perms, they produce the same code
        examples = generate_examples(target_total=10)
        assert len(examples) == 1
        assert examples[0]["nim_code"] == "Same code"

def test_generate_examples_target_limit():
    """Test that the number of examples generated respects the target limit calculations."""
    def gen():
        for i in range(100):
            yield {"var": str(i)}

    t = TemplateDef(
        name="test_limit",
        tags=["tag4"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code="Code: {var}",
        generator=gen
    )
    with patch('generate_dataset.TEMPLATES', [t]):
        # target_per_t = max(250, (target_total // len(TEMPLATES)) * 10)
        # 1 template, target_total = 10 -> max(250, 100) = 250
        # Since perms only has 100 items, we get 100
        examples = generate_examples(target_total=10)
        assert len(examples) == 100

        def large_gen():
             for i in range(400):
                  yield {"var": str(i)}

        t2 = TemplateDef(
            name="test_limit2",
            tags=["tag4"],
            prompts=["Prompt: {var}"],
            thinking="Thinking: {var}",
            code="Code: {var}",
            generator=large_gen
        )
        with patch('generate_dataset.TEMPLATES', [t2]):
            # 1 template, target_total = 10 -> max(250, 100) = 250
            # Since perms has 400 items, it should be limited to 250
            examples2 = generate_examples(target_total=10)
            assert len(examples2) == 250

def test_generate_examples_async_multiplier():
    """Test that templates with 'async' in name get 3x multiplier."""
    def gen():
        for i in range(1000):
            yield {"var": str(i)}

    t = TemplateDef(
        name="test_async_limit",
        tags=["tag5"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code="Code: {var}",
        generator=gen
    )
    with patch('generate_dataset.TEMPLATES', [t]):
        # 1 template, target_total = 10
        # target_per_t = max(250, 100) = 250
        # since 'async' is in name, target_per_t *= 3 -> 750
        examples = generate_examples(target_total=10)
        assert len(examples) == 750

def test_generate_examples_multi_multiplier():
    """Test that templates with 'multi' or 'os_json_strutils' in name get 3x multiplier."""
    def gen():
        for i in range(1000):
            yield {"var": str(i)}

    t1 = TemplateDef(
        name="test_multi_limit",
        tags=["tag6"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code="Code1: {var}",
        generator=gen
    )

    t2 = TemplateDef(
        name="test_os_json_strutils_limit",
        tags=["tag7"],
        prompts=["Prompt: {var}"],
        thinking="Thinking: {var}",
        code="Code2: {var}",
        generator=gen
    )

    with patch('generate_dataset.TEMPLATES', [t1]):
        examples1 = generate_examples(target_total=10)
        assert len(examples1) == 750

    with patch('generate_dataset.TEMPLATES', [t2]):
        examples2 = generate_examples(target_total=10)
        assert len(examples2) == 750
