from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class ExecutionStatus(str):
    DISCOVERED = "DISCOVERED"
    QUEUED = "QUEUED"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    APPROVED = "APPROVED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"

class ApprovalStatus(str):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class ExecutionRequest(ContractModel):
    schema_version: str = "1.0"
    request_id: str = Field(default_factory=lambda: f"exec_{uuid4().hex}")
    actor: str
    source: str
    tool_name: str
    operation: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    target: Optional[str] = None
    resource: Optional[str] = None
    risk_class: str = "LOW"
    approval_required: bool = True
    idempotency_key: Optional[str] = None
    timeout_seconds: Optional[float] = None
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    mission_id: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)

class ExecutionResult(ContractModel):
    schema_version: str = "1.0"
    request_id: str
    success: bool
    status: str
    message: str = ""
    stdout: Optional[str] = None
    structured_data: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    audit_event_id: Optional[str] = None
    correlation_id: Optional[str] = None

class ToolDescriptor(ContractModel):
    schema_version: str = "1.0"
    name: str
    description: str
    input_schema: Dict[str, Any]
    capabilities: List[str] = Field(default_factory=list)
    risk_class: str = "LOW"
    approval_policy: str = "REQUIRED"
    allowed_transports: List[str] = Field(default_factory=list)
    version: str = "1.0"

class ApprovalRequest(ContractModel):
    schema_version: str = "1.0"
    approval_id: str = Field(default_factory=lambda: f"approval_{uuid4().hex}")
    request_id: Optional[str] = None
    mission_id: Optional[str] = None
    requested_by: str
    summary: str
    diff_preview: Optional[str] = None
    risk_class: str = "LOW"
    impact: str = "LOW"
    created_at: datetime = Field(default_factory=utc_now)
    expires_at: Optional[datetime] = None
    status: str = ApprovalStatus.PENDING

class ApprovalDecision(ContractModel):
    schema_version: str = "1.0"
    approval_id: str
    decision: Literal["APPROVED", "REJECTED", "CANCELLED"]
    decided_by: str
    decided_at: datetime = Field(default_factory=utc_now)
    reason: Optional[str] = None
    correlation_id: Optional[str] = None

class EventEnvelope(ContractModel):
    schema_version: str = "1.0"
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=utc_now)
    source: str
    target: str
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    priority: str = "LOW"
    scope: str = "local"
    domain: str = "general"
    ttl: int = 3600
    ecosystem: str = "core"
    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    parent_trace_id: Optional[str] = None
    depth: int = 0

class MissionReference(ContractModel):
    schema_version: str = "1.0"
    mission_id: str
    goal: Optional[str] = None
    status: Optional[str] = None
    correlation_id: Optional[str] = None

class MissionState(ContractModel):
    schema_version: str = "1.0"
    mission_id: str
    goal: str
    description: str = ""
    status: str
    progress: float = 0.0
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
