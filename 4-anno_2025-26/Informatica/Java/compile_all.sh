#!/bin/bash
mkdir -p build_logs
find . -name "src" -type d | while read src_dir; do
  project_dir=$(dirname "$src_dir")
  project_name=$(basename "$project_dir")
  echo "Compiling $project_dir..."
  mkdir -p "$project_dir/bin"
  javac -Xlint:all -d "$project_dir/bin" "$src_dir"/*.java > "build_logs/${project_name}_compile.log" 2>&1
  if [ $? -ne 0 ]; then
    echo "FAILED: $project_dir"
  else
    echo "SUCCESS: $project_dir"
  fi
done
