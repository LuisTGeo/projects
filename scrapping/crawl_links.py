from urllib.parse import urlparse

from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

# from llm_engineering.application.crawlers.dispatcher import CrawlerDispatcher


from scrapping.crawler_dispatcher import CrawlerDispatcher


def crawl_links(user: str, links: list[str]) -> Annotated[list[str], "crawled_links"]:
    dispatcher = CrawlerDispatcher.build().register_linkedin().register_medium().register_github()

    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successfull_crawls = 0
    for link in tqdm(links):
        successfull_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
        successfull_crawls += successfull_crawl

        metadata = _add_to_metadata(metadata, crawled_domain, successfull_crawl)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)

    logger.info(f"Successfully crawled {successfull_crawls} / {len(links)} links.")

    return links


def _crawl_link(dispatcher: CrawlerDispatcher, link: str, user: UserDocument) -> tuple[bool, str]:
    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:
        crawler.extract(link=link, user=user)

        return (True, crawler_domain)
    except Exception as e:
        logger.error(f"An error occurred while crowling: {e!s}")

        return (False, crawler_domain)


def _add_to_metadata(metadata: dict, domain: str, successfull_crawl: bool) -> dict:
    if domain not in metadata:
        metadata[domain] = {}
    metadata[domain]["successful"] = metadata.get(domain, {}).get("successful", 0) + successfull_crawl
    metadata[domain]["total"] = metadata.get(domain, {}).get("total", 0) + 1

    return metadata


links = ['https://mlabonne.github.io/blog/posts/2024-07-29_Finetune_Llama31.html', 'https://mlabonne.github.io/blog/posts/2024-07-15_The_Rise_of_Agentic_Data_Generation.html', 'https://maximelabonne.substack.com/p/uncensor-any-llm-with-abliteration-d30148b7d43e', 'https://maximelabonne.substack.com/p/create-mixtures-of-experts-with-mergekit-11b318c99562', 'https://maximelabonne.substack.com/p/merge-large-language-models-with-mergekit-2118fb392b54', 'https://maximelabonne.substack.com/p/fine-tune-a-mistral-7b-model-with-direct-preference-optimization-708042745aac', 'https://maximelabonne.substack.com/p/exllamav2-the-fastest-library-to-run-llms-32aeda294d26', 'https://maximelabonne.substack.com/p/quantize-llama-models-with-ggml-and-llama-cpp-3612dfbcc172', 'https://maximelabonne.substack.com/p/a-beginners-guide-to-llm-fine-tuning-4bae7d4da672', 'https://maximelabonne.substack.com/p/graph-convolutional-networks-introduction-to-gnns-24b3f60d6c95', 'https://maximelabonne.substack.com/p/4-bit-quantization-with-gptq-36b0f4f02c34', 'https://maximelabonne.substack.com/p/fine-tune-your-own-llama-2-model-in-a-colab-notebook-df9823a04a32', 'https://maximelabonne.substack.com/p/introduction-to-weight-quantization-2494701b9c0c', 'https://maximelabonne.substack.com/p/decoding-strategies-in-large-language-models-9733a8f70539', 'https://maximelabonne.substack.com/p/the-art-of-spending-optimizing-your-marketing-budget-with-nonlinear-optimization-6c8a39afb3c2', 'https://maximelabonne.substack.com/p/create-a-bot-to-find-diamonds-in-minecraft-d836606a993a', 'https://maximelabonne.substack.com/p/constraint-programming-67ac16fa0c81', 'https://maximelabonne.substack.com/p/how-to-design-the-most-powerful-graph-neural-network-3d18b07a6e66', 'https://maximelabonne.substack.com/p/introduction-to-graphsage-in-python-a9e7f9ecf9d7', 'https://maximelabonne.substack.com/p/graph-attention-networks-in-python-975736ac5c0c', 'https://maximelabonne.substack.com/p/integer-programming-vs-linear-programming-in-python-f1be5bb4e60e', 'https://maximelabonne.substack.com/p/introduction-to-linear-programming-in-python-9261e7eb44b', 'https://maximelabonne.substack.com/p/what-is-a-tensor-in-deep-learning-6dedd95d6507', 'https://maximelabonne.substack.com/p/efficiently-iterating-over-rows-in-a-pandas-dataframe-7dd5f9992c01', 'https://maximelabonne.substack.com/p/q-learning-for-beginners-2837b777741', 'https://maximelabonne.substack.com/p/how-to-start-machine-learning-for-developers-in-2022-390af12b193f']