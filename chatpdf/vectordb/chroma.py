from langchain_community.vectorstores.chroma import Chroma
from typing import List
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from file import file


# 常量
DEFAULT_K = 4


class ChromaDB:
    def __init__(
        self, 
        splitter, 
        model_name: str = "BAAI/bge-base-en-v1.5", 
        device: str = "cpu",
        similarity_top_k: int = 20,
        normalize_embeddings: bool = True,
    ) -> None:

        self._similarity_top_k = similarity_top_k

        # embedding function
        self.embedding_function = self.get_embedding_function(model_name, device, normalize_embeddings)
        self.splitter = splitter
        self.db = None


    def get_embedding_function(self, model_name, device, normalize_embeddings) -> HuggingFaceEmbeddings:
        model_kwargs = {"device": device}
        encode_kwargs = {"normalize_embeddings": normalize_embeddings}
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,  # Provide the pre-trained model's path
            model_kwargs=model_kwargs,  # Pass the model configuration options
            encode_kwargs=encode_kwargs,  # Pass the encoding options
        )
        return embeddings


    # 初始化文件夹其中的数据
    def init_files(self, folder_path: str):
        """加载文件"""
        documents = file.load_from_folder(folder_path)
        documents = self.splitter.split_documents(documents)
        self.db = Chroma.from_documents(documents, self.embedding_function)


    # 在运行期间更新“单个”文档
    def add_single_file(self, path: str):
        document = file.load_single_file(path)
        self.db.add_documents(document)


    def similarity_search(self, query: str) -> List[Document]:
        return self.db.similarity_search(query, self._similarity_top_k)
