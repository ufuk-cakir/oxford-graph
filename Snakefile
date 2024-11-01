configfile: "config.yaml"

rule all:
    input:
        config["plot_file"]

rule scrape_supervisors:
    output:
        config["scraped_file"]
    params:
        base_url=config["base_url"]
    shell:
        "python src/supervisor_scraper.py {params.base_url} {output[0]}"

rule fetch_supervisor_details:
    input:
        config["scraped_file"]
    output:
        config["detailed_file"]
    shell:
        "python src/description_scraper.py {input} {output}"

rule extract_keywords:
    input:
        config["detailed_file"]
    output:
        config["keywords_file"]
    shell:
        "python src/extract_keywords.py {input} {output}"
        

rule plot_graph:
    input:
        config["keywords_file"]
    output:
        config["plot_file"]
    shell:
        "python src/plot_graph.py {input} {output}"