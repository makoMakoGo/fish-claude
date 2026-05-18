#!/usr/bin/env bash
input=$(cat)

jq_value() {
  local query=$1
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$input" | jq -r "$query" 2>/dev/null
  fi
}

short_path() {
  local path=$1
  local home=${HOME:-/home/travis}

  if [ -z "$path" ] || [ "$path" = "null" ]; then
    path=$(pwd)
  fi

  if [ "$path" = "$home" ]; then
    printf '~'
  elif [[ "$path" == "$home/"* ]]; then
    printf '~/%s' "${path#"$home"/}"
  else
    printf '%s' "$path"
  fi
}

model=$(jq_value '.model.display_name // .model.id // empty')
if [ -z "$model" ] || [ "$model" = "null" ]; then
  model="model"
fi

context=$(jq_value '.context.display // empty')
if [ -n "$context" ] && [ "$context" != "null" ]; then
  model="$model $context"
fi

cwd=$(jq_value '.cwd // .workspace.current_dir // empty')
dir=$(short_path "$cwd")

git_segment=
if command -v git >/dev/null 2>&1 && git -C "$cwd" --no-optional-locks rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
  if [ -z "$branch" ]; then
    branch=$(git -C "$cwd" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
  fi

  status=$(git -C "$cwd" --no-optional-locks status --porcelain=v1 --branch 2>/dev/null)
  header=${status%%$'\n'*}
  ahead=0
  behind=0
  staged=0
  worktree=0
  untracked=0
  conflicts=0

  if [[ "$header" =~ ahead[[:space:]]+([0-9]+) ]]; then
    ahead=${BASH_REMATCH[1]}
  fi
  if [[ "$header" =~ behind[[:space:]]+([0-9]+) ]]; then
    behind=${BASH_REMATCH[1]}
  fi

  while IFS= read -r line; do
    [ -z "$line" ] && continue
    [[ "$line" == "## "* ]] && continue

    x=${line:0:1}
    y=${line:1:1}
    xy=$x$y

    if [ "$xy" = "??" ]; then
      untracked=$((untracked + 1))
      continue
    fi
    if [[ "$x" = "U" || "$y" = "U" || "$xy" = "AA" || "$xy" = "DD" ]]; then
      conflicts=$((conflicts + 1))
    fi
    if [[ "$x" != " " && "$x" != "?" ]]; then
      staged=$((staged + 1))
    fi
    if [[ "$y" != " " && "$y" != "?" ]]; then
      worktree=$((worktree + 1))
    fi
  done <<<"$status"

  details=()
  [ "$ahead" -gt 0 ] && details+=("↑$ahead")
  [ "$behind" -gt 0 ] && details+=("↓$behind")
  [ "$staged" -gt 0 ] && details+=("+$staged")
  [ "$worktree" -gt 0 ] && details+=("~$worktree")
  [ "$untracked" -gt 0 ] && details+=("?$untracked")
  [ "$conflicts" -gt 0 ] && details+=("!$conflicts")

  if [ "${#details[@]}" -gt 0 ]; then
    git_segment="git:$branch ${details[*]}"
  else
    git_segment="git:$branch ✓"
  fi
fi

magenta='\033[01;35m'
blue='\033[01;34m'
green='\033[01;32m'
reset='\033[00m'

if [ -n "$git_segment" ]; then
  printf '%b[%s]%b %b%s%b %b%s%b\n' "$magenta" "$model" "$reset" "$blue" "$dir" "$reset" "$green" "$git_segment" "$reset"
else
  printf '%b[%s]%b %b%s%b\n' "$magenta" "$model" "$reset" "$blue" "$dir" "$reset"
fi
