import analyzer
machines=analyzer.load_valid_rows("production.csv")
analysis=analyzer.machines_analyzer(machines)
analyzer.result(analysis)
analyzer.save_report(analysis,"result.csv")


