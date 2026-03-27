"""
Limitations and Safety Considerations for Autonomous Agents

This script explores the critical limitations, safety concerns, and ethical
considerations when building and deploying autonomous agents. It demonstrates
safety mechanisms, failure modes, and best practices for responsible AI development.

Key Topics Covered:
1. Technical limitations of current autonomous agents
2. Safety mechanisms and guardrails
3. Cost management and resource constraints
4. Ethical considerations and responsible deployment
5. Failure analysis and recovery strategies
6. Monitoring and observability
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Import our autonomous agent components
from utils.autogpt_tools import SafetyConfig, AutoGPTTools

# Load environment variables
load_dotenv()


class RiskLevel(Enum):
    """Risk levels for autonomous agent operations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FailureMode(Enum):
    """Common failure modes for autonomous agents"""
    PLANNING_FAILURE = "planning_failure"
    EXECUTION_FAILURE = "execution_failure"
    TOOL_FAILURE = "tool_failure"
    MEMORY_CORRUPTION = "memory_corruption"
    COST_EXHAUSTION = "cost_exhaustion"
    SAFETY_VIOLATION = "safety_violation"
    GOAL_DRIFT = "goal_drift"
    INFINITE_LOOP = "infinite_loop"


@dataclass
class SafetyMetrics:
    """Metrics for tracking safety and performance"""
    total_operations: int = 0
    failed_operations: int = 0
    safety_violations: int = 0
    cost_exceeded: bool = False
    goal_achieved: bool = False
    execution_time: float = 0.0
    error_rate: float = 0.0
    
    def calculate_error_rate(self) -> float:
        """Calculate the error rate"""
        if self.total_operations == 0:
            return 0.0
        return self.failed_operations / self.total_operations
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reporting"""
        return {
            "total_operations": self.total_operations,
            "failed_operations": self.failed_operations,
            "safety_violations": self.safety_violations,
            "cost_exceeded": self.cost_exceeded,
            "goal_achieved": self.goal_achieved,
            "execution_time": self.execution_time,
            "error_rate": self.calculate_error_rate()
        }


@dataclass
class SafetyPolicy:
    """Safety policy for autonomous agent operations"""
    max_cost_per_session: float = 10.0  # USD
    max_execution_time: int = 1800  # seconds (30 minutes)
    max_api_calls_per_minute: int = 60
    allowed_operations: List[str] = field(default_factory=lambda: [
        "web_search", "file_read", "file_write", "analysis", "planning"
    ])
    blocked_operations: List[str] = field(default_factory=lambda: [
        "system_modify", "network_scan", "file_delete_system", "install_packages"
    ])
    required_human_approval: List[str] = field(default_factory=lambda: [
        "file_delete", "network_connect", "system_config"
    ])
    risk_threshold: float = 0.7  # Maximum acceptable risk level


class SafetyMonitor:
    """Monitor and enforce safety policies for autonomous agents"""
    
    def __init__(self, policy: SafetyPolicy):
        self.policy = policy
        self.metrics = SafetyMetrics()
        self.start_time = time.time()
        self.api_call_timestamps = []
        self.violation_log = []
    
    def check_operation_safety(self, operation: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if an operation is safe to execute"""
        self.metrics.total_operations += 1
        
        # Check if operation is blocked
        if operation in self.policy.blocked_operations:
            violation = f"Operation {operation} is blocked by policy"
            self._log_violation(violation, RiskLevel.HIGH)
            return False, violation
        
        # Check if operation requires human approval
        if operation in self.policy.required_human_approval:
            return self._request_human_approval(operation, context)
        
        # Check rate limiting
        if not self._check_rate_limit():
            violation = "Rate limit exceeded for API calls"
            self._log_violation(violation, RiskLevel.MEDIUM)
            return False, violation
        
        # Check cost limits
        if self._check_cost_limits():
            violation = "Cost limits exceeded"
            self._log_violation(violation, RiskLevel.HIGH)
            return False, violation
        
        # Check time limits
        if self._check_time_limits():
            violation = "Execution time limit exceeded"
            self._log_violation(violation, RiskLevel.MEDIUM)
            return False, violation
        
        # Assess operation risk
        risk_level = self._assess_operation_risk(operation, context)
        if risk_level == RiskLevel.CRITICAL:
            violation = f"Operation {operation} assessed as critical risk"
            self._log_violation(violation, RiskLevel.CRITICAL)
            return False, violation
        
        return True, "Operation approved"
    
    def _request_human_approval(self, operation: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Request human approval for sensitive operations"""
        print(f"\n🔒 HUMAN APPROVAL REQUIRED")
        print(f"Operation: {operation}")
        print(f"Context: {json.dumps(context, indent=2)}")
        print(f"Risk Level: {self._assess_operation_risk(operation, context).value}")
        
        while True:
            choice = input("Approve this operation? (yes/no): ").strip().lower()
            if choice == 'yes':
                return True, "Human approved"
            elif choice == 'no':
                violation = f"Human rejected operation: {operation}"
                self._log_violation(violation, RiskLevel.MEDIUM)
                return False, violation
            else:
                print("Please enter 'yes' or 'no'")
    
    def _check_rate_limit(self) -> bool:
        """Check if API call rate limit is exceeded"""
        now = time.time()
        # Remove calls older than 1 minute
        self.api_call_timestamps = [t for t in self.api_call_timestamps if now - t < 60]
        
        if len(self.api_call_timestamps) >= self.policy.max_api_calls_per_minute:
            return False
        
        self.api_call_timestamps.append(now)
        return True
    
    def _check_cost_limits(self) -> bool:
        """Check if cost limits are exceeded"""
        # Simplified cost calculation - in practice, you'd track actual API costs
        estimated_cost = self.metrics.total_operations * 0.001  # Rough estimate
        
        if estimated_cost > self.policy.max_cost_per_session:
            self.metrics.cost_exceeded = True
            return True
        
        return False
    
    def _check_time_limits(self) -> bool:
        """Check if execution time limit is exceeded"""
        elapsed = time.time() - self.start_time
        if elapsed > self.policy.max_execution_time:
            self.metrics.execution_time = elapsed
            return True
        
        return False
    
    def _assess_operation_risk(self, operation: str, context: Dict[str, Any]) -> RiskLevel:
        """Assess the risk level of an operation"""
        # High-risk operations
        high_risk_ops = ["file_delete", "network_connect", "system_modify"]
        if operation in high_risk_ops:
            return RiskLevel.HIGH
        
        # Medium-risk operations
        medium_risk_ops = ["web_search", "file_write", "api_call"]
        if operation in medium_risk_ops:
            return RiskLevel.MEDIUM
        
        # Low-risk operations
        low_risk_ops = ["analysis", "planning", "memory_read"]
        if operation in low_risk_ops:
            return RiskLevel.LOW
        
        # Default to medium risk
        return RiskLevel.MEDIUM
    
    def _log_violation(self, violation: str, risk_level: RiskLevel):
        """Log a safety violation"""
        self.violation_log.append({
            "timestamp": datetime.now().isoformat(),
            "violation": violation,
            "risk_level": risk_level.value
        })
        self.metrics.safety_violations += 1
        
        print(f"🚨 SAFETY VIOLATION: {violation}")
    
    def record_operation_result(self, success: bool, operation: str):
        """Record the result of an operation"""
        if not success:
            self.metrics.failed_operations += 1
    
    def get_safety_report(self) -> Dict[str, Any]:
        """Generate a comprehensive safety report"""
        self.metrics.execution_time = time.time() - self.start_time
        self.metrics.error_rate = self.metrics.calculate_error_rate()
        
        return {
            "metrics": self.metrics.to_dict(),
            "policy": {
                "max_cost": self.policy.max_cost_per_session,
                "max_time": self.policy.max_execution_time,
                "max_api_rate": self.policy.max_api_calls_per_minute
            },
            "violations": self.violation_log,
            "assessment": self._generate_safety_assessment()
        }
    
    def _generate_safety_assessment(self) -> str:
        """Generate an overall safety assessment"""
        if self.metrics.safety_violations > 0:
            return "UNSAFE - Safety violations detected"
        elif self.metrics.error_rate > 0.2:
            return "RISKY - High error rate detected"
        elif self.metrics.cost_exceeded:
            return "RISKY - Cost limits exceeded"
        else:
            return "SAFE - No safety issues detected"


class FailureAnalyzer:
    """Analyze and learn from autonomous agent failures"""
    
    def __init__(self):
        self.failure_log = []
        self.patterns = {}
    
    def analyze_failure(self, failure_mode: FailureMode, context: Dict[str, Any], 
                       error_message: str) -> Dict[str, Any]:
        """Analyze a specific failure"""
        failure_entry = {
            "timestamp": datetime.now().isoformat(),
            "failure_mode": failure_mode.value,
            "context": context,
            "error_message": error_message,
            "analysis": self._analyze_failure_pattern(failure_mode, context, error_message)
        }
        
        self.failure_log.append(failure_entry)
        self._update_patterns(failure_mode, context)
        
        return failure_entry
    
    def _analyze_failure_pattern(self, failure_mode: FailureMode, 
                                context: Dict[str, Any], error_message: str) -> str:
        """Analyze the pattern behind a failure"""
        patterns = {
            FailureMode.PLANNING_FAILURE: "Planning failures often occur when goals are ambiguous or when the agent lacks domain knowledge",
            FailureMode.EXECUTION_FAILURE: "Execution failures typically result from tool unavailability or incorrect tool usage",
            FailureMode.TOOL_FAILURE: "Tool failures happen when external services are unavailable or return unexpected results",
            FailureMode.MEMORY_CORRUPTION: "Memory corruption occurs when the agent's state becomes inconsistent or corrupted",
            FailureMode.COST_EXHAUSTION: "Cost exhaustion happens when the agent makes too many API calls or expensive operations",
            FailureMode.SAFETY_VIOLATION: "Safety violations occur when the agent attempts operations that violate safety policies",
            FailureMode.GOAL_DRIFT: "Goal drift happens when the agent deviates from the original objective",
            FailureMode.INFINITE_LOOP: "Infinite loops occur when the agent gets stuck in repetitive patterns"
        }
        
        return patterns.get(failure_mode, "Unknown failure pattern")
    
    def _update_patterns(self, failure_mode: FailureMode, context: Dict[str, Any]):
        """Update failure pattern statistics"""
        key = failure_mode.value
        if key not in self.patterns:
            self.patterns[key] = {"count": 0, "contexts": []}
        
        self.patterns[key]["count"] += 1
        
        # Extract key context features
        context_features = {
            "goal": context.get("goal", "unknown"),
            "iteration": context.get("iteration", 0),
            "tools_used": context.get("tools_used", [])
        }
        
        self.patterns[key]["contexts"].append(context_features)
    
    def get_failure_report(self) -> Dict[str, Any]:
        """Generate a comprehensive failure analysis report"""
        total_failures = len(self.failure_log)
        
        if total_failures == 0:
            return {"status": "no_failures", "message": "No failures recorded"}
        
        # Calculate failure statistics
        failure_stats = {}
        for mode, data in self.patterns.items():
            failure_stats[mode] = {
                "count": data["count"],
                "percentage": (data["count"] / total_failures) * 100
            }
        
        # Identify most common failure modes
        sorted_failures = sorted(failure_stats.items(), 
                               key=lambda x: x[1]["count"], reverse=True)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(sorted_failures)
        
        return {
            "total_failures": total_failures,
            "failure_modes": failure_stats,
            "most_common": sorted_failures[:3] if sorted_failures else [],
            "recommendations": recommendations,
            "recent_failures": self.failure_log[-5:]  # Last 5 failures
        }
    
    def _generate_recommendations(self, sorted_failures: List[Tuple[str, Dict]]) -> List[str]:
        """Generate recommendations based on failure patterns"""
        recommendations = []
        
        if not sorted_failures:
            return recommendations
        
        top_failure = sorted_failures[0][0]
        
        if top_failure == FailureMode.PLANNING_FAILURE.value:
            recommendations.extend([
                "Improve goal clarity and specificity",
                "Add domain knowledge to the agent",
                "Implement better planning validation"
            ])
        elif top_failure == FailureMode.EXECUTION_FAILURE.value:
            recommendations.extend([
                "Add more robust error handling",
                "Improve tool selection logic",
                "Add fallback mechanisms"
            ])
        elif top_failure == FailureMode.TOOL_FAILURE.value:
            recommendations.extend([
                "Add tool availability checks",
                "Implement tool retry mechanisms",
                "Add alternative tools for critical operations"
            ])
        elif top_failure == FailureMode.COST_EXHAUSTION.value:
            recommendations.extend([
                "Implement better cost tracking",
                "Add cost optimization strategies",
                "Set stricter cost limits"
            ])
        elif top_failure == FailureMode.SAFETY_VIOLATION.value:
            recommendations.extend([
                "Review and tighten safety policies",
                "Add better risk assessment",
                "Implement pre-operation safety checks"
            ])
        
        return recommendations


class EthicalFramework:
    """Framework for ethical considerations in autonomous agents"""
    
    def __init__(self):
        self.ethical_guidelines = [
            "Autonomous agents should not cause harm to humans",
            "Agents should be transparent about their capabilities and limitations",
            "Privacy and data protection should be prioritized",
            "Agents should not discriminate or show bias",
            "Human oversight should be maintained for critical decisions",
            "Agents should be accountable for their actions"
        ]
    
    def assess_operation_ethics(self, operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the ethical implications of an operation"""
        assessment = {
            "operation": operation,
            "ethical_score": 0.8,  # Default score
            "concerns": [],
            "recommendations": []
        }
        
        # Check for privacy concerns
        if "personal_data" in str(context).lower() or "private" in str(context).lower():
            assessment["concerns"].append("Potential privacy concerns")
            assessment["ethical_score"] -= 0.2
            assessment["recommendations"].append("Ensure data anonymization")
        
        # Check for bias concerns
        if "discriminate" in str(context).lower() or "bias" in str(context).lower():
            assessment["concerns"].append("Potential bias concerns")
            assessment["ethical_score"] -= 0.3
            assessment["recommendations"].append("Review for algorithmic bias")
        
        # Check for harmful operations
        harmful_keywords = ["harm", "damage", "destroy", "attack", "exploit"]
        context_str = str(context).lower()
        for keyword in harmful_keywords:
            if keyword in context_str:
                assessment["concerns"].append(f"Potentially harmful operation: {keyword}")
                assessment["ethical_score"] -= 0.4
                assessment["recommendations"].append(f"Review necessity of {keyword} operation")
        
        return assessment
    
    def get_ethical_report(self) -> Dict[str, Any]:
        """Generate an ethical compliance report"""
        return {
            "guidelines": self.ethical_guidelines,
            "compliance_status": "Compliant",
            "last_review": datetime.now().isoformat(),
            "recommendations": [
                "Regular ethical audits",
                "Human-in-the-loop for sensitive operations",
                "Transparency in agent decision-making"
            ]
        }


def demonstrate_safety_features():
    """Demonstrate the safety and monitoring features"""
    print("🛡️  Autonomous Agent Safety & Limitations Demo")
    print("=" * 60)
    
    # Initialize safety components
    safety_policy = SafetyPolicy(
        max_cost_per_session=5.0,
        max_execution_time=300,  # 5 minutes
        max_api_calls_per_minute=10
    )
    
    safety_monitor = SafetyMonitor(safety_policy)
    failure_analyzer = FailureAnalyzer()
    ethical_framework = EthicalFramework()
    
    print("\n1. Testing Safety Policies...")
    
    # Test blocked operation
    safe, message = safety_monitor.check_operation_safety("system_modify", {})
    print(f"Blocked operation test: {safe} - {message}")
    
    # Test allowed operation
    safe, message = safety_monitor.check_operation_safety("web_search", {"query": "test"})
    print(f"Allowed operation test: {safe} - {message}")
    
    # Test rate limiting
    for i in range(12):  # Exceed the limit of 10
        safe, message = safety_monitor.check_operation_safety("api_call", {})
        if i == 10:
            print(f"Rate limit test: {safe} - {message}")
    
    print("\n2. Testing Failure Analysis...")
    
    # Simulate various failures
    failure_analyzer.analyze_failure(
        FailureMode.PLANNING_FAILURE,
        {"goal": "ambiguous goal", "iteration": 1},
        "Unable to create plan from ambiguous goal"
    )
    
    failure_analyzer.analyze_failure(
        FailureMode.TOOL_FAILURE,
        {"tool": "web_search", "iteration": 3},
        "Web search API returned error 503"
    )
    
    failure_analyzer.analyze_failure(
        FailureMode.COST_EXHAUSTION,
        {"cost": 5.50, "limit": 5.0, "iteration": 15},
        "Cost limit exceeded"
    )
    
    failure_report = failure_analyzer.get_failure_report()
    print(f"Total failures: {failure_report['total_failures']}")
    print(f"Most common failure: {failure_report['most_common'][0] if failure_report['most_common'] else 'None'}")
    
    print("\n3. Testing Ethical Assessment...")
    
    # Test ethical assessment
    ethical_assessment = ethical_framework.assess_operation_ethics(
        "data_analysis",
        {"data_type": "personal_data", "purpose": "marketing"}
    )
    print(f"Ethical score: {ethical_assessment['ethical_score']}")
    print(f"Concerns: {ethical_assessment['concerns']}")
    
    print("\n4. Generating Safety Report...")
    
    safety_report = safety_monitor.get_safety_report()
    print(f"Safety Assessment: {safety_report['assessment']}")
    print(f"Total Operations: {safety_report['metrics']['total_operations']}")
    print(f"Safety Violations: {safety_report['metrics']['safety_violations']}")
    
    print("\n5. Key Limitations of Current Autonomous Agents...")
    
    limitations = [
        "🧠 **Context Window Limitations**: Agents can only maintain limited context",
        "💰 **Cost Constraints**: API calls and operations incur costs",
        "⏱️ **Time Constraints**: Long-running tasks may hit time limits",
        "🔧 **Tool Dependencies**: Reliance on external services and APIs",
        "🎯 **Goal Ambiguity**: Poorly defined goals lead to poor execution",
        "🔄 **Error Propagation**: Early errors can cascade through execution",
        "🛡️ **Safety Trade-offs**: Strict safety limits may restrict capabilities",
        "📊 **Monitoring Challenges**: Hard to detect subtle failures or drift"
    ]
    
    for limitation in limitations:
        print(f"  {limitation}")
    
    print("\n6. Best Practices for Safe Autonomous Agents...")
    
    best_practices = [
        "✅ **Clear Goal Definition**: Be specific about objectives and constraints",
        "✅ **Safety First**: Implement comprehensive safety policies and monitoring",
        "✅ **Cost Management**: Track and limit API usage and costs",
        "✅ **Error Handling**: Build robust error recovery mechanisms",
        "✅ **Human Oversight**: Maintain human-in-the-loop for critical decisions",
        "✅ **Regular Monitoring**: Continuously monitor agent behavior and performance",
        "✅ **Ethical Guidelines**: Follow ethical principles in agent design",
        "✅ **Testing**: Thoroughly test agents before deployment"
    ]
    
    for practice in best_practices:
        print(f"  {practice}")
    
    print("\n" + "=" * 60)
    print("🎯 Safety & Limitations Demo Complete!")
    print("Remember: Autonomous agents are powerful tools that require")
    print("careful consideration of safety, ethics, and limitations.")


def main():
    """Main function to run the safety and limitations demonstration"""
    demonstrate_safety_features()


if __name__ == "__main__":
    main()
