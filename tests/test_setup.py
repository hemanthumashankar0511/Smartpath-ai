import os
import sqlite3

# Ollama & LangChain imports
try:
    from langchain_community.llms import Ollama
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    ollama_installed = True
except ImportError:
    ollama_installed = False


def test_ollama():
    if not ollama_installed:
        print("[FAIL] langchain-ollama not installed.")
        return
    try:
        llm = Ollama(model="llama3.2:3b")
        prompt = PromptTemplate(input_variables=["question"], template="Q: {question}\nA:")
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run("What is AI?")
        print("[PASS] Ollama + LangChain chain working. Sample response:")
        print(response[:200] + ("..." if len(response) > 200 else ""))
    except Exception as e:
        print(f"[FAIL] Ollama/LangChain test failed: {e}")

def test_sqlite():
    try:
        db_path = os.path.join("data", "test.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)")
        c.execute("INSERT INTO test_table (name) VALUES (?)", ("SmartPath Test",))
        conn.commit()
        c.execute("SELECT * FROM test_table")
        rows = c.fetchall()
        print(f"[PASS] SQLite connection and CRUD working. Rows: {rows}")
        c.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()
        os.remove(db_path)
    except Exception as e:
        print(f"[FAIL] SQLite test failed: {e}")

def main():
    print("--- SmartPath AI Setup Test ---")
    test_ollama()
    test_sqlite()

if __name__ == "__main__":
    main() 