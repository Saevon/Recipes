




# Value Exists
has_repo = session.query(models.Repo.repo_id).filter_by(ext_repo_id=ext_repo_id).scalar() is not None
