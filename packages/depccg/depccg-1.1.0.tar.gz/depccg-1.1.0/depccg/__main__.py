
import argparse
import sys
import logging
import json
from lxml import etree

from .parser import EnglishCCGParser, JapaneseCCGParser
from .printer import print_
from depccg.tokens import Token, english_annotator, japanese_annotator, annotate_XX
from .download import download, load_model_directory, SEMANTIC_TEMPLATES, model_is_available, AVAILABLE_MODEL_VARIANTS
from .lang import BINARY_RULES
from .utils import read_partial_tree, read_weights
from .lang import en_default_binary_rules, ja_default_binary_rules
from .combinator import HeadfirstCombinator

Parsers = {'en': EnglishCCGParser, 'ja': JapaneseCCGParser}

# disable lengthy allennlp logs
logging.getLogger('allennlp').setLevel(logging.ERROR)


def main(args):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        level=logging.CRITICAL if args.silent else logging.INFO)

    if args.weights is not None:
        probs, tag_list = read_weights(args.weights)
    else:
        probs, tag_list = None, None

    binary_rules = BINARY_RULES[args.lang]
    if args.lang == 'en':
        assert not args.format in ['ccg2lambda', 'jigg_xml_ccg2lambda'] or args.annotator, \
                f'Specify --annotator argument in using "{args.format}" output format'
        annotate_fun = english_annotator.get(args.annotator, annotate_XX)

    elif args.lang == 'ja':
        assert not args.format in ['ccg2lambda', 'jigg_xml_ccg2lambda'] or args.tokenize, \
                f'Cannot specify --pre-tokenized argument using "{args.format}" output format'
        annotate_fun = japanese_annotator[args.annotator] if args.tokenize else annotate_XX
    else:
        assert False

    if args.root_cats is not None:
        args.root_cats = args.root_cats.split(',')

    kwargs = dict(
        unary_penalty=args.unary_penalty,
        nbest=args.nbest,
        binary_rules=binary_rules,
        possible_root_cats=args.root_cats,
        pruning_size=args.pruning_size,
        beta=args.beta,
        use_beta=not args.disable_beta,
        use_seen_rules=not args.disable_seen_rules,
        use_category_dict=not args.disable_category_dictionary,
        max_length=args.max_length,
        max_steps=args.max_steps,
        gpu=args.gpu
    )

    model_name = f'{args.lang}[{args.model}]'
    if args.model and model_is_available(model_name):
        model, config = load_model_directory(model_name)
    else:
        def_model, config = load_model_directory(args.lang)
        model = args.model or def_model

    parser = Parsers[args.lang].from_json(
                args.config or config, model, **kwargs)

    fin = sys.stdin if args.input is None else open(args.input)

    if args.input is not None:
        input_type = open(args.input)
    elif not sys.stdin.isatty():
        input_type = sys.stdin
    else:
        # reading from keyboard
        input_type = None
        sys.stdout.flush()
        sys.stderr.flush()
        logging.getLogger().setLevel(logging.CRITICAL)

    while True:
        fin = [line for line in ([input()] if input_type is None else input_type) if len(line.strip()) > 0]
        if len(fin) == 0:
            break

        if args.input_format == 'POSandNERtagged':
            tagged_doc = [[Token.from_piped(token) for token in sent.strip().split(' ')] for sent in fin]
            doc = [' '.join(token.word for token in sent) for sent in tagged_doc]
            res = parser.parse_doc(doc,
                                   probs=probs,
                                   tag_list=tag_list,
                                   batchsize=args.batchsize)
        elif args.input_format == 'json':
            doc = [json.loads(line) for line in fin]
            tagged_doc = annotate_fun(
                [[word for word in sent['words'].split(' ')] for sent in doc])
            res = parser.parse_json(doc)
        elif args.input_format == 'partial':
            doc, constraints = zip(*[read_partial_tree(l.strip()) for l in fin])
            tagged_doc = annotate_fun(doc)
            res = parser.parse_doc(doc,
                                   probs=probs,
                                   tag_list=tag_list,
                                   batchsize=args.batchsize,
                                   constraints=constraints)
        else:
            doc = [l.strip() for l in fin]
            doc = [sentence for sentence in doc if len(sentence) > 0]
            tagged_doc = annotate_fun([[word for word in sent.split(' ')] for sent in doc],
                                      tokenize=args.tokenize)
            if args.tokenize:
                tagged_doc, doc = tagged_doc
            res = parser.parse_doc(doc,
                                   probs=probs,
                                   tag_list=tag_list,
                                   batchsize=args.batchsize)

        semantic_templates = args.semantic_templates or SEMANTIC_TEMPLATES.get(args.lang)
        print_(res, tagged_doc,
                format=args.format,
                lang=args.lang,
                semantic_templates=semantic_templates)
        
        if input_type is None:
            sys.stdout.flush()
        else:
            break


def add_common_parser_arguments(parser):
    parser.add_argument('-c',
                        '--config',
                        help='json config file specifying the set of unary rules used, etc.')
    parser.add_argument('-m',
                        '--model',
                        help='path to model directory')
    parser.add_argument('-i',
                        '--input',
                        default=None,
                        help='a file with tokenized sentences in each line')
    parser.add_argument('-w',
                        '--weights',
                        default=None,
                        help='a file that contains weights (p_tag, p_dep)')
    parser.add_argument('--gpu',
                        type=int,
                        default=-1,
                        help='specify gpu id')
    parser.add_argument('--batchsize',
                        type=int,
                        default=32,
                        help='batchsize in supertagger')
    parser.add_argument('--nbest',
                        type=int,
                        default=1,
                        help='output N best parses')
    parser.add_argument('-I',
                        '--input-format',
                        default='raw',
                        choices=['raw', 'POSandNERtagged', 'json', 'partial'],
                        help='input format')
    parser.add_argument('--root-cats',
                        default=None,
                        help='allow only these categories at the root of a tree.')
    parser.add_argument('--unary-penalty',
                        default=0.1,
                        type=float,
                        help='penalty to use a unary rule')
    parser.add_argument('--beta',
                        default=0.00001,
                        type=float,
                        help='parameter used to filter categories with lower probabilities')
    parser.add_argument('--pruning-size',
                        default=50,
                        type=int,
                        help='use only the most probable supertags per word')
    parser.add_argument('--disable-beta',
                        action='store_true',
                        help='disable the use of the beta value')
    parser.add_argument('--disable-category-dictionary',
                        action='store_true',
                        help='disable a category dictionary that maps words to most likely supertags')
    parser.add_argument('--disable-seen-rules',
                        action='store_true',
                        help='')
    parser.add_argument('--max-length',
                        default=250,
                        type=int,
                        help='give up parsing a sentence that contains more words than this value')
    parser.add_argument('--max-steps',
                        default=10000000,
                        type=int,
                        help='give up parsing when the number of times of popping agenda items exceeds this value')
    parser.add_argument('--semantic-templates',
                        help='semantic templates used in "ccg2lambda" format output')
    parser.add_argument('--silent',
                        action='store_true')
    parser.set_defaults(func=main)

    subparsers = parser.add_subparsers()
    download_parser = subparsers.add_parser('download')
    download_parser.add_argument('VARIANT',
                                 nargs='?',
                                 default=None,
                                 choices=AVAILABLE_MODEL_VARIANTS[parser.get_default('lang')])
    download_parser.set_defaults(func=lambda args: download(args.lang, args.VARIANT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A* CCG parser')
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    english_parser = subparsers.add_parser('en')
    english_parser.set_defaults(lang='en')
    add_common_parser_arguments(english_parser)
    english_parser.add_argument('-a',
                                '--annotator',
                                default=None,
                                help='annotate POS, named entity, and lemmas using this library',
                                choices=english_annotator.keys())
    english_parser.add_argument('-f',
                                '--format',
                                default='auto',
                                choices=['auto', 'auto_extended', 'deriv', 'xml', 'conll', 'html', 'prolog',
                                         'jigg_xml', 'ptb', 'ccg2lambda', 'jigg_xml_ccg2lambda', 'json'],
                                help='output format')
    english_parser.add_argument('--tokenize',
                                action='store_true',
                                help='tokenize input sentences')
    english_parser.add_argument('--disfluency',
                                action='store_true',
                                help='perform disfluency detection')

    japanese_parser = subparsers.add_parser('ja')
    japanese_parser.set_defaults(lang='ja')
    add_common_parser_arguments(japanese_parser)
    japanese_parser.add_argument('-a',
                                 '--annotator',
                                 default='janome',
                                 help='annotate POS, named entity, and lemmas using this library',
                                 choices=japanese_annotator.keys())
    japanese_parser.add_argument('-f',
                                 '--format',
                                 default='ja',
                                 choices=['auto', 'deriv', 'ja', 'conll', 'html', 'jigg_xml', 'ptb',
                                          'ccg2lambda', 'jigg_xml_ccg2lambda', 'json', 'prolog'],
                                 help='output format')
    japanese_parser.add_argument('--pre-tokenized',
                                 dest='tokenize',
                                 action='store_false',
                                 help='the input is pre-tokenized (for running parsing experiments etc.)')
    japanese_parser.set_defaults(disfluency=False)

    args = parser.parse_args()
    args.func(args)



