# main.py
from Code import model_trainer
from Code import model_validate
from Code import model_predict


def main():
    print("Menu:")
    print("1. Train Model")
    print("2. Validate Model")
    print("3. Predict Model")

    try:
        option = int(input("Enter your choice (1/2/3): "))

        if option == 1:
            model_trainer.main()
        elif option == 2:
            model_validate.main()
        elif option == 3:
            model_predict.main()
        else:
            print("Invalid option. Please enter 1, 2, or 3.")
    except ValueError:
        print("Invalid input. Please enter a valid option.")


if __name__ == '__main__':
    main()
