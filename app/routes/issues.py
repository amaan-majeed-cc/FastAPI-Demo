import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueUpdate, IssueOut, IssueStatus
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

issues = [
    {"id": 1, "title": "Issue 1", "description": "Description 1"},
    {"id": 2, "title": "Issue 2", "description": "Description 2"},
    {"id": 3, "title": "Issue 3", "description": "Description 3"},
]

@router.get("/", response_model=list[IssueOut])
def get_issues():
    """Retrieve all issues"""
    return load_data()

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """Create a new issue"""
    issue_data = load_data()
    new_issue = {
        "id": len(issue_data) + 1,
        "title": payload.title,
        "description": payload.description,
        "status": IssueStatus.open,
        "priority": payload.priority,
    }
    issue_data.append(new_issue)
    save_data(issue_data)
    return new_issue

# Update
@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: int, payload: IssueUpdate):
    """Update an issue"""
    issue_data = load_data()
    issue = next((issue for issue in issue_data if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    issue.update(payload.model_dump())
    save_data(issue_data)
    return issue

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: int):
    """Delete an issue"""
    issue_data = load_data()
    issue = next((issue for issue in issue_data if issue["id"] == issue_id), None)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    issue_data.remove(issue)
    save_data(issue_data)
    return {"message": "Issue deleted successfully"}
