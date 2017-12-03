import logging

from mad_invest.trainner import main

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] : %(message)s'")

    main()
