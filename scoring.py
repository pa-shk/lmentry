import argparse

from lmentry.analysis.accuracy import flexible_scoring
from tasks.task_utils import get_tasks_names, task_groups, all_tasks
from lmentry.model_manager import get_short_model_names


def parse_arguments():
  parser = argparse.ArgumentParser(
    description="CLI for scoring all or specified LMentry predictions using the default file locations",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument("-m", "--model_names", nargs="+", type=str, default=None,
                      help="Names of models which statistics were collected and should evaluate. "
                           "If it is None the predictions directory is analized and evailable model-statistics are evaluated")
  parser.add_argument('-t', '--task_names', nargs="+", type=str, default=None,
                      help="If need to evaluate specified set of tasks set their names or name(s) of specified task set(s). "
                           f"Task set names should be from the list: {task_groups.keys()}. "
                           f"Task names should be from the list: {all_tasks}. "
                           "By default it tries to score all predicted tasks for specified models")
  parser.add_argument("-n", "--num-procs", type=int, default=1,
                      help="The number of processes to use when scoring the predictions. "
                           "Can be up to the number of models you want to evaluate * 41.")
  parser.add_argument('--use_vllm', type=bool, default=False,
                      help="Whether to score vLLM predictions.")
  parser.add_argument("-f", "--forced_scoring", action="store_true", default=False,
                      help="If scoring has been done for specified task it skips it. This flag allows to redo ready scoring")
  return parser.parse_args()


def main():
  args = parse_arguments()

  task_names = get_tasks_names(args.task_names)

  model_names = get_short_model_names(args.model_names)
  flexible_scoring(
    task_names=task_names,
    model_names=model_names,
    num_processes=args.num_procs,
    use_vllm=args.use_vllm,
    forced_scoring=args.forced_scoring
  )


if __name__ == "__main__":
  main()
