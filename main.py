from src.App import TicketToRideNoAi, TicketToRideTrainAi


def main():
    """
    Main function for project
    :return:
    """
    # app = TicketToRideNoAi()
    app = TicketToRideTrainAi()
    app.run()


if __name__ == '__main__':
    main()
