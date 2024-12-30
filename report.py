import pygit2


def get_latest_tag_for_submodule(repo, submodule_path):
    """
    Get the latest tag for a submodule in the repository.
    """
    submodule_repo_path = repo.workdir + submodule_path
    try:
        submodule_repo = pygit2.Repository(submodule_repo_path)
    except Exception as e:
        print(f"Error accessing submodule {submodule_path}: {e}")
        return None

    tags = submodule_repo.references.glob('refs/tags/*')
    latest_tag = None
    latest_time = 0
    for tag_ref in tags:
        tag = submodule_repo.lookup_reference(tag_ref)
        tag_commit = tag.peel(pygit2.Commit)
        if tag_commit.commit_time > latest_time:
            latest_time = tag_commit.commit_time
            latest_tag = tag.shorthand

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
            if entry.type == pygit2.GIT_OBJECT_TREE:  # Fixed constant name
                # Handle regular files or directories (no need to check)
                continue
            if entry.type == pygit2.GIT_OBJECT_BLOB:
                # Handle blobs (actual file contents)
                continue

            # Check if entry is a submodule (new or updated)
            if entry.name in repo.submodules:
                submodule = repo.submodules[entry.name]
                # Compare the commit ID of the submodule with its current HEAD ID
                if entry.id != submodule.head_id:  # Fixed attribute
                    updated_submodules[entry.name] = entry.id.hex  # Record the update
            else:
                # Newly added submodule
                updated_submodules[entry.name] = entry.id.hex

        # Move to the previous commit
        if current_commit.parents:
            current_commit = current_commit.parents[0]
        else:
            break

    return updated_submodules


def main(repo_path, start_commit_hash, end_commit_hash):
    try:
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

    except Exception as e:
        print(f"Error: {e}")


# Example usage
repo_path = "D:\\Haim\\git\\super"
start_commit_hash = "139eaa6a46eed3c4f5f81242a4dd0be8269613a1"  # Replace with actual start commit hash - older
end_commit_hash = "e3d27ccecae41194a9f16c405afc29dd832e4c7f"  # Replace with actual end commit hash - newer

main(repo_path, start_commit_hash, end_commit_hash)
