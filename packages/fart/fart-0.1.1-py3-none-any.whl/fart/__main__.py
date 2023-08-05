import argparse
import fart

def main():
    #=== Make CLI
    parser = argparse.ArgumentParser(description='Fart on your docs')
    arg = parser.add_argument
    arg('text', nargs='*', type=str, help='text to fart')
    arg('-f', '--font', default=None, type=str, choices=fart.FONT_NAMES,
        help='name of the figlet font used for fart')

    arg('-n', '--no_copy', action='store_true',
        help='don\'t copy fart to clipboard')

    arg('-s', '--sample', action='store_true',
        help='print sample of all figlet fonts')

    arg('-c', '--cap', default=fart.CAP, type=str,
        help='<cap> character that is appended to ends of text lines <cap> ')

    arg('-l', '--line', default=fart.LINE, type=str,
        help='character that makes lines, eg \'~\': #~~~~~~~~#')

    #=== Parse args
    args = parser.parse_args()

    # sample
    sample = args.sample
    if sample:
        fart.sample_farts('Sample')
        return 0

    # primary args
    text = ' '.join(args.text)
    font_name = args.font
    cap  = args.cap
    line = args.line
    copy = not args.no_copy

    #=== Fart
    fart.fart(text, font_name, cap, line, copy)
    return 0


if __name__ == '__main__':
    ret = main()
