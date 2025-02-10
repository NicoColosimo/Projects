import pytest
from unittest.mock import patch
from project import main, Game, Store, Item


@pytest.fixture
def game():
    """Fixture to make game instance."""
    return Game()


def test_main():
    """Test main; should terminate when '7'."""
    with patch('builtins.input', return_value='7'), patch('builtins.print') as mock_print:
        main()  # Call the main function
        # Check if the "Goodbye" message was printed which will indicate game over
        mock_print.assert_any_call("Exiting the game. Goodbye!")



def test_show_inventory(game):
    """Test show_inventory by capturing output."""
    with patch('builtins.print') as mock_print:
        game.show_inventory()  # Ensure this method prints the inventory
        # Check that the correct print statement was called
        mock_print.assert_any_call("\nApple: $1.0 (Stock: 100)")
        mock_print.assert_any_call("\nBanana: $0.5 (Stock: 100)")

def test_show_menu():
    """See if menu showed correctly."""
    with patch('builtins.input', return_value='1'): # Use our return value of 1 to see if it works
        choice = Game().show_menu()
        assert choice == '1'


def test_handle_choice(game):
    """test handle_choice with user input."""
    # Simulate choosing 1 to simulate the day
    with patch('builtins.input', return_value='1'):
        result = game.handle_choice('1')
        assert result is True

    # Simulate quitting with 7
    result = game.handle_choice('7')
    assert result is False


def test_start_day(game):
    """Test if the day activities are correct simulations."""
    initial_cleanliness = game.store.cleanliness
    game.start_day()

    # Ensure the cleanliness decreases by 25 after a day
    assert game.store.cleanliness == initial_cleanliness - 25


def test_buy_items(game):
    """Test if the buy_items function is correct when buying items."""
    # Test side effects with more inputs such as y for continuing and 3 for amount of Bananas
    with patch('builtins.input', side_effect=['Apple', '2', 'y', 'Banana', '3', 'n']):
        game.buy_items()


@pytest.mark.parametrize("choice, expected_result", [
    ('1', True),  # Simulate a day should return True to continue the game
    ('7', False),  # Quit the game should return False
])
def test_handle_choice_with_params(game, choice, expected_result):
    """Test handle_choice function with parameterized inputs."""
    result = game.handle_choice(choice)
    assert result == expected_result
