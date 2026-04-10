## PRP Ralph Loop Activated

**Plan**: {file_path}
**Iteration**: 1
**Max iterations**: {N}

The stop hook is now active. When you try to exit:

- If validations incomplete → same prompt fed back
- If all validations pass → loop exits

To monitor: `cat .github/prp-ralph.state.md`
To cancel: `/prp-ralph-cancel`

______________________________________________________________________

CRITICAL REQUIREMENTS:

- Work through ALL tasks in the plan
- Run ALL validation commands
- Fix failures before proceeding
- Only output <promise>COMPLETE</promise> when ALL validations pass
- Do NOT lie to exit - the loop continues until genuinely complete

______________________________________________________________________

Starting iteration 1...
