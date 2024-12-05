import argparse
from configuration import Configuration

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kubernetes CLI Tool.")

    parser.add_argument(
        "--kubeconfig", type=str, help="ruta al archivo kubeconfig", default=None
    )
    args = parser.parse_args()

    if args.kubeconfig is None:
        flags = ""
    else:
        flags = f"--kubeconfig {args.kubeconfig}"

    Configuration().set_flags(flags)

    from main import main
    main()