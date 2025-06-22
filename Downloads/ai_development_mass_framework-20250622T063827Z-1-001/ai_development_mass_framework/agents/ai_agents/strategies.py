from typing import Dict, Any, List

class ConflictResolutionStrategy:
    def resolve(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        raise NotImplementedError

class FirstComeFirstServeStrategy(ConflictResolutionStrategy):
    def resolve(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Returns the first conflict as the resolution
        return conflicts[0] if conflicts else {}

class MajorityVoteStrategy(ConflictResolutionStrategy):
    def resolve(self, conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Example: returns the most common conflict detail
        from collections import Counter
        if not conflicts:
            return {}
        details = [str(conflict['details']) for conflict in conflicts if 'details' in conflict]
        most_common = Counter(details).most_common(1)
        for conflict in conflicts:
            if str(conflict.get('details')) == most_common[0][0]:
                return conflict
        return conflicts[0]