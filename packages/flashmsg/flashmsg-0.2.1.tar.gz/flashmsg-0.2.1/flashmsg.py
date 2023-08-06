from colorama import Fore
import sys
import logging


def flash_msg(msg,
              sign='*',
              bar_length=5,
              bar_name='',
              log=False,
              exit_code=False,
              color=''):
    '''

    Function to display a message in a flash style.
    Daniel C. Baeriswyl

    :param msg: list or str of messages
    :param sign: string of desired space filler
    :param bar_length: length of side bars
    :param bar_name: name display on bar
    :param log: do you use a logger ? if so, log=True
    :param exit_code: Possible to exit code after message. Exit if exit_code =True
    :param color: Choose your color/ red, blue or green
    :return:
    '''


    if type(msg) == float:
        msg = [msg]
    if type(msg) == str:
        msg = [msg]

    msg = [str(i) for i in msg]

    if bar_name == '':
        # If there is no bar name
        bar_name = sign
        spec = sign * bar_length

        right_side = ' ' \
                     + sign * bar_length
    else:

        remainder = len(sign * bar_length \
                    + ' ' \
                    + bar_name ) % bar_length
        if remainder >0:
            extra = ' ' * (len(sign)-1 - remainder)

        else:
            extra = ''

        spec = sign * bar_length \
               + ' ' \
               + bar_name \
               + ' ' \
               + extra \
               + sign * bar_length

        right_side = ' '+ " "*(remainder-1) \
                     + sign * bar_length

    left_side = spec \
                + ' '

    x = 0
    for i in msg:
        if len(i) > x:
            x = len(i)
    # x is the length of the message
    x1 = x \
         + len(left_side)
    # x1 lenght of message plut left side
    x2 = x \
         + len(left_side) \
         + len(right_side)
    # x2 is length of message plus left and righ side

    if color == 'red':
        c1 = Fore.RED
    elif color == 'green':
        c1 = Fore.GREEN
    elif color == 'blue':
        c1 = Fore.BLUE
    else:
        c1 = Fore.RESET

    c2 = Fore.RESET

    if not log:

        # prints the top bar

        top_bottom = x2*sign
        top_bottom = top_bottom[:x2]
        print(c1,
              top_bottom,
              c2)

        # for each message
        for i in msg:

            #calculate white space if messages have different lengths
            whitespace = ' ' * (x1
                                - (len(i)
                                   + len(left_side)))

            if i == msg[0]:
                print(c1,
                      left_side
                      + i
                      + whitespace
                      + right_side, c2)
            else:
                fill_up = sign * len(spec)
                print(c1,
                      fill_up[0:len(spec)]
                      + ' '
                      + i
                      + whitespace
                      + right_side, c2)


        print(c1, top_bottom, c2)

    else:
        print('Logging function not fixed yet')
        # logging.info(c1 + sign * x2 + c2)
        # for i in msg:
        #     whitespace = ' ' * (x1 - (len(i) + len(spec1)))
        #     if bar_name == '':
        #         logging.info(c1 + spec1 + i + whitespace + spec2 + c2)
        #     else:
        #         if i == msg[0]:
        #             logging.info(c1 + spec1 + i + whitespace + spec2 + c2)
        #         else:
        #             logging.info(c1 + sign * (len(spec1) - 1) + ' ' + i + whitespace + spec2 + c2)
        # logging.info(c1 + sign * x2 + c2)
        pass

    if exit_code:
        sys.exit(1)
