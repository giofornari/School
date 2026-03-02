#!/bin/bash
mkdir -p build_logs
find . -name "src" -type d | while read src_dir; do
  project_dir=$(dirname "$src_dir")
  project_name=$(basename "$project_dir")

  # Skip bin or build directories if they contain a src folder for some reason
  if [[ "$project_dir" == *"/bin" ]] || [[ "$project_dir" == *"/build" ]]; then
    continue
  fi

  echo "Compiling $project_dir..."

  if [ -f "$project_dir/pom.xml" ]; then
    # Maven project
    mvn -f "$project_dir/pom.xml" clean compile > "build_logs/${project_name}_compile.log" 2>&1
    if [ $? -ne 0 ]; then
      echo "FAILED (Maven): $project_dir"
    else
      echo "SUCCESS (Maven): $project_dir"
    fi
  else
    # Plain Java project
    mkdir -p "$project_dir/bin"
    find "$src_dir" -name "*.java" > sources.txt
    if [ -s sources.txt ]; then
      javac -Xlint:all -d "$project_dir/bin" @sources.txt > "build_logs/${project_name}_compile.log" 2>&1
      if [ $? -ne 0 ]; then
        echo "FAILED: $project_dir"
      else
        echo "SUCCESS: $project_dir"
      fi
    else
      echo "SKIPPED (No Java files): $project_dir"
    fi
    rm sources.txt
  fi
done
