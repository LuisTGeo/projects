from urllib.parse import urlparse

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers.html2text import Html2TextTransformer
from loguru import logger


class CustomArticleCrawler:

    def __init__(self) -> None:
        super().__init__()

    def extract(self, link: str, **kwargs) -> dict:
        logger.info(f"Starting scrapping article: {link}")

        loader = AsyncHtmlLoader([link])
        docs = loader.load()

        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(docs)
        doc_transformed = docs_transformed[0]

        content = {
            "Title": doc_transformed.metadata.get("title"),
            "Subtitle": doc_transformed.metadata.get("description"),
            "Content": doc_transformed.page_content,
            "language": doc_transformed.metadata.get("language"),
        }

        parsed_url = urlparse(link)
        platform = parsed_url.netloc

        user = kwargs["user"]
        instance = {
            "content": content,
            "link": link,
            "platform": platform,
            "author_iduser": id,
            "author_full_name": user.full_name,
        }

        logger.info(f"Finished scrapping custom article: {link} ::: {instance}")
        return instance

    def extract_multiple(self, links: list, **kwargs) -> list:
        results = []
        for link in links:
            try:
                result = self.extract(link, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Error scraping {link}: {e}")
        return results



if __name__ == "__main__":
    # Dummy user object with a 'full_name' attribute
    class User:
        def __init__(self, full_name):
            self.full_name = full_name

    # Instantiate user and article links
    user = User(full_name="Jane Doe")


    links = ['https://mlabonne.github.io/blog/posts/2024-07-29_Finetune_Llama31.html',
             'https://mlabonne.github.io/blog/posts/2024-07-15_The_Rise_of_Agentic_Data_Generation.html',
             'https://maximelabonne.substack.com/p/uncensor-any-llm-with-abliteration-d30148b7d43e',
             'https://maximelabonne.substack.com/p/create-mixtures-of-experts-with-mergekit-11b318c99562',
             'https://maximelabonne.substack.com/p/merge-large-language-models-with-mergekit-2118fb392b54',
             'https://maximelabonne.substack.com/p/fine-tune-a-mistral-7b-model-with-direct-preference-optimization-708042745aac',
             'https://maximelabonne.substack.com/p/exllamav2-the-fastest-library-to-run-llms-32aeda294d26',
             'https://maximelabonne.substack.com/p/quantize-llama-models-with-ggml-and-llama-cpp-3612dfbcc172',
             'https://maximelabonne.substack.com/p/a-beginners-guide-to-llm-fine-tuning-4bae7d4da672',
             'https://maximelabonne.substack.com/p/graph-convolutional-networks-introduction-to-gnns-24b3f60d6c95',
             'https://maximelabonne.substack.com/p/4-bit-quantization-with-gptq-36b0f4f02c34',
             'https://maximelabonne.substack.com/p/fine-tune-your-own-llama-2-model-in-a-colab-notebook-df9823a04a32',
             'https://maximelabonne.substack.com/p/introduction-to-weight-quantization-2494701b9c0c',
             'https://maximelabonne.substack.com/p/decoding-strategies-in-large-language-models-9733a8f70539',
             'https://maximelabonne.substack.com/p/the-art-of-spending-optimizing-your-marketing-budget-with-nonlinear-optimization-6c8a39afb3c2',
             'https://maximelabonne.substack.com/p/create-a-bot-to-find-diamonds-in-minecraft-d836606a993a',
             'https://maximelabonne.substack.com/p/constraint-programming-67ac16fa0c81',
             'https://maximelabonne.substack.com/p/how-to-design-the-most-powerful-graph-neural-network-3d18b07a6e66',
             'https://maximelabonne.substack.com/p/introduction-to-graphsage-in-python-a9e7f9ecf9d7',
             'https://maximelabonne.substack.com/p/graph-attention-networks-in-python-975736ac5c0c',
             'https://maximelabonne.substack.com/p/integer-programming-vs-linear-programming-in-python-f1be5bb4e60e',
             'https://maximelabonne.substack.com/p/introduction-to-linear-programming-in-python-9261e7eb44b',
             'https://maximelabonne.substack.com/p/what-is-a-tensor-in-deep-learning-6dedd95d6507',
             'https://maximelabonne.substack.com/p/efficiently-iterating-over-rows-in-a-pandas-dataframe-7dd5f9992c01',
             'https://maximelabonne.substack.com/p/q-learning-for-beginners-2837b777741',
             'https://maximelabonne.substack.com/p/how-to-start-machine-learning-for-developers-in-2022-390af12b193f']

    # Initialize the crawler and run `extract_multiple`
    crawler = CustomArticleCrawler()
    articles_data = crawler.extract_multiple(links, user=user)

    # Print out each article's data
    for article in articles_data:
        print(article)