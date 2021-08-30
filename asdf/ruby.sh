echo
echo "${bold}Setting up ruby...${clear}"
gem install solargraph # code completion, documentation, and static analysis
gem install ruby-debug-ide # an interface which glues ruby-debug to IDEs
gem install debase -v '>= 0.2.5.beta' # implementation of standard Ruby debugger
# installed latest ruby version and set it as default
asdf plugin add ruby
asdf install ruby latest > /dev/null
asdf global ruby latest
