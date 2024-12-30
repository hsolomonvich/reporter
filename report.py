import pygit2


def get_latest_tag_for_submodule(repo, submodule_path):
    """
    Get the latest tag for a submodule in the repository.
    """
    submodule_repo = repo[submodule_path].repo
    tags = submodule_repo.tags
    latest_tag = None
    for tag_name in sorted(tags, key=lambda t: tags[t].commit.time, reverse=True):
        latest_tag = tag_name
        break
    return latest_tag


def get_submodules_updated_in_range(repo, start_commit, end_commit):
    """
    Get the submodules updated in the specified commit range.
    """
    updated_submodules = {}

    # Get the commit objects for start and end commits
    start_commit_obj = repo.get(start_commit)
    end_commit_obj = repo.get(end_commit)

    # Iterate over commits in the range
    current_commit = end_commit_obj
    while current_commit != start_commit_obj:
        for entry in current_commit.tree:
            if entry.mode == pygit2.GIT_OBJ_COMMIT:
                continue  # Skip non-submodule entries
            if entry.name in repo.submodules:
                submodule = repo.submodules[entry.name]
                if entry.id != submodule.hex:
                    updated_submodules[entry.name] = entry.id.hex  # Record the update
        # Move to the previous commit
        if current_commit.parents:
            current_commit = current_commit.parents[0]
        else:
            break

    return updated_submodules


def main(repo_path, start_commit_hash, end_commit_hash):
    # Open the repository
    repo = pygit2.Repository(repo_path)

    # Get the start and end commits
    start_commit = start_commit_hash
    end_commit = end_commit_hash

    # Get submodules updated in the specified commit range
    updated_submodules = get_submodules_updated_in_range(repo, start_commit, end_commit)

    print(f"Submodules updated between commits {start_commit} and {end_commit}:")

    for submodule_name, updated_commit_id in updated_submodules.items():
        print(f"Submodule: {submodule_name}, Updated Commit: {updated_commit_id}")
        # Fetch the latest tag for the submodule
        latest_tag = get_latest_tag_for_submodule(repo, submodule_name)
        if latest_tag:
            print(f"Latest Tag for {submodule_name}: {latest_tag}")
        else:
            print(f"No tags found for submodule: {submodule_name}")
        print('---')



# Example usage
repo_path = "D:\Haim\git\super"
start_commit_hash = "139eaa6a46eed3c4f5f81242a4dd0be8269613a1"  # Replace with actual start commit hash - older
end_commit_hash = "e3d27ccecae41194a9f16c405afc29dd832e4c7f"  # Replace with actual end commit hash - newer

main(repo_path, start_commit_hash, end_commit_hash)
