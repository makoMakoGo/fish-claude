# Completion Discipline

<important if="you are writing code, fixing bugs, debugging, or verifying changes">
- Do not treat a runnable patch, green local test, typecheck, or single reproduced case as completion unless it verifies the user-visible requirement.
- Before editing, identify the requirement, affected path, and verification that would prove the actual behavior.
- If the diagnosis is uncertain, contested, or contradicted by runtime evidence, gather deciding evidence before applying a fix.
- If a fix fails verification, stop patching: revert, re-read, or re-plan from confirmed facts before changing more code.
- Report completion only with observed evidence; state remaining verification gaps as gaps.
</important>
