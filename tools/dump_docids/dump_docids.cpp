#include <iostream>

#include "indri/CompressedCollection.hpp"
#include "indri/LocalQueryServer.hpp"
#include "indri/Parameters.hpp"
#include "indri/Repository.hpp"


int main(int argc, char** argv)
{
    if (argc < 2) {
	std::cerr << "usage: dump_docids <repo>" << std::endl;
	return 1;
    }

    std::string repoPath(argv[1]);

    indri::collection::Repository repo;
    repo.openRead(repoPath);

    indri::server::LocalQueryServer server(repo);
    indri::collection::CompressedCollection* collection = repo.collection();

    int N = server.documentCount();
    for (int i = 1; i <= N; ++i) {
	std::string name = collection->retrieveMetadatum(i, "docno");
	std::cout << name << std::endl;
    }

    return 0;
}
